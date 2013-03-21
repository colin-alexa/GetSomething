<?php
	session_start();
	if(isset($_SESSION["state"]))
	{
		if($_SESSION["state"] == "login")
		{
			if(!isset($_GET["maxPrice"]))
				$maxPrice = "1";
			else
			{
				$maxPrice = $_GET["maxPrice"];
				$maxPrice = (int)$maxPrice;
				$output = exec("python launch.py " . $maxPrice . " " . $_SESSION["token"]);
				
			}
		}
	}
?>
<script>
	window.location = 'index.php?output=' + '<?php echo $output; ?>';
</script>
