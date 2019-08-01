<?php

/**
 * Class Template
 *
 * @property Page $page
 * @property string|null $template
 */
class Template
{
    protected $page;

    /**
     * Template constructor.
     *
     * @param Page $page
     */
    public function __construct($page)
    {
        $this->page = $page;
    }

    /**
     * Render the head/top of a template.
     *
     * @return void
     */
    public function renderTop()
    {
        $pageName = $this->page->getTitle();

        foreach ($this->page->getScripts() as $scriptName) {
            $$scriptName = true;
        }
        $script = $this->page->getCustomScript();

        $banner = $this->page->getBanner();

        require __DIR__ . '/templates/top.php';
    }

    /**
     * Render the bottom of a template.
     *
     * @return void
     */
    public function renderBottom()
    {
        foreach ($this->page->getScripts() as $scriptName) {
            $$scriptName = true;
        }

        require __DIR__ . '/templates/bottom.php';
    }
}
