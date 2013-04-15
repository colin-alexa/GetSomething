<!DOCTYPE html>
<?php
	session_start(); 
	if(isset($_SESSION["token"]))
		$_SESSION["state"] = "login";	
	elseif(!isset($_SESSION["state"]))
		$_SESSION["state"] = "unknown";
?>
<html>
  <head>
    <title>GetSomething</title>
    <meta name="GetSomething application" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link href="assets/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <style>
    #mainBox {
    border-radius: 10px;
    background: whitesmoke;
    }
    </style>
  </head>
  <body style="background:skyblue;>
  <div class="navbar">
    <div class="navbar-inner">
      <h3 class="brand" href="#">GetSomething: surprise yourself!</h3>
	 
    </div>
  </div>
<div class="container">
  <div>
    
    <h1 class="text-center">Hello, world!</h1>

    
  </div>
 <div class="container">
 <div class="row-fluid">
  <div class="span6 offset3" id="mainBox" style="background:whitesmoke;">
  <form>
    <fieldset>
    <h5 style="padding-left:7%">GetSomething</h5>
    <hr/>
      <div class="row-fluid">
      <div class="span4 offset2">
        <label>Max price</label>
        <input type="text" placeholder="$1.00">
      </div>
      <div class="span3 offset3">
         <?php
			if($_SESSION["state"] != "login")
			{
				$loginUrl = exec("python LoginWrapper.py");
		?>
				<a href="<?php echo $loginUrl; ?>">Login</a>
	    <?php
			}
			else
			{
	   ?>
				<a href="logout.php">Logout</a>
		<?php } ?>
      </div>
    </div>
    </div>
  </fieldset>
  </form>

 </div>
 </div>
 </div>

    <script>function popup(){alert("Hey! Listen!")}</script>
    <script src="../assets/js/jquery.js"></script>
    <script src="../assets/js/bootstrap-transition.js"></script>
    <script src="../assets/js/bootstrap-alert.js"></script>
    <script src="../assets/js/bootstrap-modal.js"></script>
    <script src="../assets/js/bootstrap-dropdown.js"></script>
    <script src="../assets/js/bootstrap-scrollspy.js"></script>
    <script src="../assets/js/bootstrap-tab.js"></script>
    <script src="../assets/js/bootstrap-tooltip.js"></script>
    <script src="../assets/js/bootstrap-popover.js"></script>
    <script src="../assets/js/bootstrap-button.js"></script>
    <script src="../assets/js/bootstrap-collapse.js"></script>
    <script src="../assets/js/bootstrap-carousel.js"></script>
    <script src="../assets/js/bootstrap-typeahead.js"></script>
  </body>
</html>   