<html>

<head>
	<title>Payment information</title>
</head>

	<body>
		<?php
		try {
			$conn = new MongoDB\Driver\Manager('mongodb://root:prisma@mongo:27017');

			$options = [
				'projection' => [],
			];
			$filter = ['id' => $_GET['acctid']];
			$query = new MongoDB\Driver\Query($filter, $options);

			$cursor = $conn->executeQuery('customers.paymentinfo', $query);
			$counter = 0;
			
			foreach ($cursor as $obj) {
				$counter++;
				echo 'Name: ' . $obj->name . '<br/>';
				echo 'Customer ID: ' . $obj->id . '<br/>';
				echo 'Card Number: ' . $obj->cc . '<br/>';
				echo 'CVV2 Code: ' . $obj->cvv2 . '<br/>';
				echo '<br/>';
			}

			echo $counter . ' document(s) found. <br/>';
			
		} catch (MongoConnectionException $e) {
			die('Error connecting to MongoDB server : ' . $e->getMessage());
		} catch (MongoException $e) {
			die('Error: ' . $e->getMessage());
		}
		?>


	</body>

</html>