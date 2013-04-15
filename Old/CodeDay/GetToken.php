<?php
	if(isset($_GET["username"]))
	{
		session_start();
	
		$username = $_GET["username"];
		$token = exec("python GetTokenWrapper.py " . $username);
		
		$_SESSION["token"] = $token;
		$_SESSION["username"] = $username;
?>
		<script>
			window.location = "index.php";
		</script>
<?php	
	}
?>
