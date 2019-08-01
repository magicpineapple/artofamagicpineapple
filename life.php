<?php

require __DIR__ . '/autoload.php';

$page = new Page('Home');
$page->addScript('index');

$page->template->renderTop();
?>

<section class="section">
	<div class="container">
		<div id="art-gallery" class="gallery">

			<div class="gallery-unit-div"><img class="gallery-unit" src='images/photoshop art/what-we-build-SMALL.jpg' /></div>

		</div>
	</div>
</section>

<?php

$page->template->renderBottom();
