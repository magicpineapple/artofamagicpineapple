<?php

require __DIR__ . '/autoload.php';

$page = new Page('Home');
$page->addScript('index');

$page->template->renderTop();
?>

<section class="section">
	<div class="container">
		<div id="art-gallery" class="gallery">

			<?php
			//Loop through each image
			include_once("colors.inc.php");
			$ex = new GetMostCommonColors();

			$files = scandir('images/art');
			foreach ($files as $file) {
				//do your work here
				echo $file; 

				$needle   = ".";

				//skip first 3 
				if( strpos( $file, $needle ) !== false) {
					$newFile = 'images/art/'.$file;
					echo $newFile;/*
				$colors = $ex->Get_Color($newFile, 5, $reduce_brightness, $reduce_gradients, $delta);
				?>
				<table>
					<tr>
						<td>Color</td>
						<td>Color Code</td>
						<td>Percentage</td>
						<td rowspan="<?php echo (($num_results > 0) ? ($num_results + 1) : 22500); ?>"><img src="images/test.jpg" alt="test image" /></td>
					</tr>
					<?php
					foreach ($colors as $hex => $count) {
						if ($count > 0) {
							echo "<tr><td style=\"background-color:#" . $hex . ";\"></td><td>" . $hex . "</td><td>$count</td></tr>";
						}
					}
					*/
				}
			
			}
				//Make 9 hue div columns 
				?>

		</div>
	</div>
</section>

<?php

$page->template->renderBottom();
