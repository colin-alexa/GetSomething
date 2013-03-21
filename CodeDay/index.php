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
  <link rel="stylesheet" type="text/css" href="layout.css" media="screen" />
    <title>GetSomething</title>
    <meta name="GetSomething application" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap -->
    <link href="assets/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <style>
    .contentBox {
    border-radius: 10px;
    background: whitesmoke;
    }
    </style>
	<script>
		function redir()
		{
			ref = "BuyProduct.php?maxPrice=" + document.getElementById("maxPrice").value;
			window.location = ref;
		}
	</script>
  </head>
  <body style="background-color:skyblue" onload="setLink()">
  <div class="navbar">
    <div class="navbar-inner">
     <h1 class="brand" href="#">GetSomething</h1>
     <div>
     <p class="text-right" style="padding-top:50px;font-size:15px;">...blindly buy something cheap on ebay
     </div>
    </div>
  </div>
  <div class="container">
  <div>
   <form>
    <h1 class="text-center" style="font-size:45px;">surprise yourself</h1>
   </form>
    
  </div>
 <div class="container">
 <div class="row-fluid">
  <div class="span6 offset3 contentBox" style="background:whitesmoke;">
  <form>
    <fieldset>
   
      <div class="row-fluid">
      
      <div class="span3 offset3">
				<h4 id="divTitle" style="padding-left:7%"></h4>
				
                <div class="span4 offset4">
                         <?php
			if($_SESSION["state"] != "login")
			{
				$loginUrl = exec("python LoginWrapper.py");
	     	?>
                <a class="text-center btn btn-primary" href="<?php echo $loginUrl;?>"   style="margin-left: 20px; width: 100px" >Login</a>
	        <?php
	     		}
	     		else
	     		{
	        ?>
				<h4 id="divTitle" style="padding-left:7%">Parameters</h4>
				<div class="span5 offset2">
					<label>max&nbsp;price</label>
					<form method="POST" action="BuyProduct.php">
						<input type="text" placeholder="1.00" id="maxPrice" value="1.00"/>
					</form>
				</div>
                <table class="table" style="padding-left:7%;border:0px;">
                 <tr>
                  <td>
				  <a class="btn btn-primary" href="logout.php">Logout</a>
                  </td>
                  <td>
                  <a class="btn btn-primary" id="link" onclick="redir();">GO</a>
                  </td>
                 </tr>
                </table>
                </div>
		<?php } ?>
      </div>
    </div>
    </div>
  </fieldset>
  </form>

 </div>
 </div>
    <?php
	if(isset($_GET["output"]))
	{
	?>
		<div class="row-fluid">
		<div class="span6 offset3 contentBox">
		<h3 style="font-size:14px;">You just bought:</h3>
	<?php
		echo $_GET["output"];
	?>
   </div>
  </div>
  <?php } ?>;
 </div>
 
    <script>function hide(id){document.getElementById(id).type="hidden"; a=document.getElementById('bigLogin');a.value='GO';}
			</script>
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
  <br>
  <center>
	<a href="#" onclick="HideMe()">Directions [+/-]</a>
	<div id="Directions" style="visibility:hidden">
		Enter in a maximum price in US dollars that you are willing to pay,
	<br>and this webappwill buy a random item from eBay.
	<br>Suprise yourself and GetSomething :)
	</div>
  </center>
  
    <script>
 function HideMe()
	{
		if (document.getElementById("Directions").style.visibility == "hidden")
			document.getElementById("Directions").style.visibility = "visible";
		else
			document.getElementById("Directions").style.visibility = "hidden";
	}
	</script>
  
  
  <center><footer></footer></center>
</html>   