<?php

/**
 * Class Page
 *
 * @property Template $template
 * @property string|null $title
 * @property array $scripts
 * @property string|null $customScript
 * @property string|null $banner
 */
class Page
{
    public $template;

    protected $title;
    protected $scripts = [];
    protected $customScript = null;
    protected $banner = null;

    /**
     * Page constructor.
     *
     * @param string|null $title
     * @param string|null $template
     */
    public function __construct($title = null, $template = 'bootstrap')
    {
        $this->title = $title;

        $this->template = new Template($this, $template);
    }

    /**
     * Get the title for this page.
     *
     * @return string|null
     */
    public function getTitle()
    {
        return $this->title;
    }

    /**
     * Set the title for this page.
     *
     * @param string|null $title
     */
    public function setTitle($title)
    {
        $this->title = $title;
    }

    /**
     * Get the scripts used on this page.
     *
     * @return array
     */
    public function getScripts()
    {
        return $this->scripts;
    }

    /**
     * Set all of the scripts used on this page.
     *
     * @param array $scripts
     * @return void
     */
    public function setScripts($scripts)
    {
        $this->scripts = $scripts;
    }

    /**
     * Add a script to use on this page.
     *
     * @param array|string|null $scripts
     * @return void
     */
    public function addScript($scripts = null)
    {
        $scripts = is_array($scripts) ? $scripts : func_get_args();

        $this->scripts = array_merge($this->scripts, $scripts);
    }

    /**
     * Check if a specific script is in use on this page.
     *
     * @param string $script
     * @return bool
     */
    public function hasScript($script)
    {
        return in_array($script, $this->scripts);
    }

    /**
     * Get the custom script used on this page.
     *
     * @return string|null
     */
    public function getCustomScript()
    {
        return $this->customScript;
    }

    /**
     * Set the custom script to be used on this page.
     *
     * @param string|null $customScript
     */
    public function setCustomScript($customScript)
    {
        $this->customScript = $customScript;
    }

    /**
     * Get the banner for this page.
     *
     * @return string|null
     */
    public function getBanner()
    {
        return $this->banner;
    }

    /**
     * Set the banner for this page.
     *
     * @param string|null $html
     */
    public function setBanner($html)
    {
        $this->banner = $html;
    }
}
