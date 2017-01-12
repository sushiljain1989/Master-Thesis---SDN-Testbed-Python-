<?php

error_reporting(E_ALL);
ini_set('display_errors', '1');
session_start();
#phpinfo();
#session_destroy();die;
if(isset($_POST['test']) && isset($_FILES))
{
	$conn = new mysqli("localhost", "root", "sunset", "jobs");

	//echo "<pre>";print_r($_FILES); echo "</pre>";
	$controllers = array("frenetic" , "pyretic" , "kinetic" , "openmul");
	
	foreach ($controllers as $key => $v ) {
		# code...
		if(array_key_exists($v, $_FILES))
		{
			//echo "Controller: " . $v . "<br>";
			//echo "Files uploaded : <br>" ; //print_r($_FILES[$v]['name']);
			//echo "<br>";
			foreach ($_FILES[$v]['name'] as $file => $value) {

				
				
				if(file_exists ( "../uploads/".$v."/".$value ) && $value !="" )
				{
					unlink("../uploads/".$v."/".$value);
				}
				move_uploaded_file($_FILES[$v]['tmp_name'][$file],"../uploads/".$v."/".$value);
				
				$status = "Pending";
				
				if($value != null && $value != "")
				{
					$stmt = $conn->prepare("INSERT INTO jobs (controller, name, status, created) VALUES (?, ?, ?, ?)");
					$date = date('Y-m-d H:i:s');
					$stmt->bind_param("ssss", $v, $value, $status, $date);
					$stmt->execute();	
					$stmt->close();
				}
				
				
				/*if(isset($_SESSION[$v]))
				{
					$_SESSION[$v][$value] = $status;
				}
				else
				{
					if($value != "" && $value != null)
					{
						
						$_SESSION[$v] = array();
						$_SESSION[$v][$value] = $status;
					}

				}*/
			}

		}
		
		
		
	}
	/*if( count($_SESSION) > 0)
	{
		#echo "<pre>";print_r($_SESSION); echo "</pre>";
		$client= new GearmanClient();
		$client->addServer();
		$data = session_id();
		$jobHandle =  $client->doBackground("reverse" , $data);
		
		#$_SESSION['gearman'] = $jobHandle;

		foreach($_SESSION as $k => $v)
  		{
  			echo "<pre>"; print_r($v); "</pre>";
  		}
	} */
	$conn->close();

	echo '<a href="index.php"> Click here to add more applications </a><br>';
	echo '<a href="status.php?format=html"> Click here to view progress </a><br>';
	die;

}

?>
<html>
<head>
	
	<script type="text/javascript" src="../jquery.js"></script>

	<script type="text/javascript">
$( document ).ready(function() {
  // Handler for .ready() called.


});
	</script>
</head>

<body>
<form action="" method="post" enctype="multipart/form-data">	
<input type="hidden" name="test" value="test">
<table border="1px;">

	<tr>
		<th>Controller</th>
		<th>Choose Application(s)</th>
		
	</tr>
	<tbody>
	<tr>
		<td>
			Frenetic
		</td>
		<td><input class="apps" type="file" name="frenetic[]" multiple></td>
		
	</tr>
	<tr>
		<td>
			Pyretic
		</td>
		<td><input class="apps" type="file" name="pyretic[]" multiple></td>
		
	</tr>
	<tr>
		<td>
			Kinetic
		</td>
		<td><input class="apps" type="file" name="kinetic[]" multiple></td>
		
	</tr>
	<tr>
		<td>
			OpenMul
		</td>
		<td><input class="apps" type="file" name="openmul[]"></td>
		
	</tr>
	</tbody>
	
</table>
<br><br>
<input type="submit"  value="Run" style="margin-left: 75px; width: 100px; height: 45px;">
</form>


</body>

</html>