<?php
error_reporting(E_ALL);
ini_set('display_errors', '1');
?>

<?php
$link = mysqli_connect("localhost", "root", "sunset", "jobs");
 
$result = mysqli_query($link, "select * from jobs ");
$myArray = array();
 if(isset($_GET['format']) && $_GET['format'] == "html")
	{ ?>

<html>
<head>

<style>
table
{
border-style:solid;
border-width:2px;
border-color:pink;
}
</style>
</head>
<body >
<?php 
		echo "<table border='1'>
		<tr>
		<th>Controller</th>
		<th>Application</th>
		<th>Status</th>
		<th>Packets Dropped</th>
		<th>Flow Rules</th>
		<th>Created at</th>
		<th>Finished at</th>
		</tr>";
		 

		while($row = mysqli_fetch_array($result,MYSQLI_ASSOC) )
		  {

				
				  echo "<tr>";
				  echo "<td>" . $row['controller'] . "</td>";
				  echo "<td>" . $row['name'] . "</td>";
				  echo "<td>" . $row['status'] . "</td>";
				  echo "<td>" . $row['pingall'] . "%</td>";
				  echo "<td>" . $row['flow_rules'] . "</td>";
				  echo "<td>" . $row['created'] . "</td>";
				  echo "<td>"; if($row['status'] != "Finished"){echo "In queue"; } else{ echo $row['finished']; } echo "</td>";
				  echo "</tr>";
				

		  }
		echo "</table>";
		?>
		<br/><br/><br/>
<a  style="margin-left:100 px;" href="status.php">Click here to refresh</a>
<br/><br/>
<a  style="margin-left:100 px;" href="index.php">Click here to add more applications</a>
</body>
</html>
		<?php 
	}

else if(isset($_GET['format']) && $_GET['format'] == "json")
		{
			while($row = mysqli_fetch_array($result,MYSQLI_ASSOC) )
		  	{
				$myArray[] = $row;	

		  	}
		  	echo json_encode($myArray);

		}
else if(isset($_GET['format']) && $_GET['format'] == "xml")
		{
			
			$xml          = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>";
			$xml         .= "<Jobs>";
			while($row = mysqli_fetch_array($result,MYSQLI_ASSOC) )
		  	{
		  	  $xml.='<Job><Controller>'.$row['controller'].'</Controller><Application>'.$row['name'].'</Application><Status>'.$row['status'].'</Status><Created>'.$row['created'].'</Created><Finished>'.$row['finished'].'</Finished></Job>';
		  	}
		  	$xml.='</Jobs>';
		  	
			$xmll = new SimpleXMLElement(trim($xml));
			echo $xmll->asXML();
		  	

		}		

mysqli_free_result($result);
mysqli_close($link);

?>
