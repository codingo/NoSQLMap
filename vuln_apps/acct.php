<html>
<head>
<title>Payment information</title>
</head>
<body>
<?php
try {
	$conn = new MongoClient();
	$db = $conn->customers;
	$collection = $db->paymentinfo;
	$search = $_GET['acctid'];
//	$criteria = array('id' => $search);
//	$fields = array('name','id','cc','cvv2');
	
	
	$cursor = $collection->find(array('id' => $search));
	
//	echo $search;
	echo $cursor->count() . ' document(s) found. <br/>';

	foreach ($cursor as $obj) {
		echo 'Name: ' . $obj['name'] . '<br/>';
		echo 'Customer ID: ' . $obj['id'] . '<br/>';
		echo 'Card Number: ' . $obj['cc'] . '<br/>';
		echo 'CVV2 Code: ' . $obj['cvv2'] . '<br/>';
		echo '<br/>';
	}
	
$conn->close();
} catch (MongoConnectionException $e) {
	die('Error connecting to MongoDB server : ' . $e->getMessage());
} catch (MongoException $e) {
	die('Error: ' . $e->getMessage());
}
?>
	

</body>
</html>