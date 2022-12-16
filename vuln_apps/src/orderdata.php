<!DOCTYPE html>
<html>
	<head>
		<title>Order Lookup</title>
	</head>
	<body>
		<?php
		if (isset($_GET['ordersearch']) && !empty($_GET['ordersearch'])) {
			try {
				$result = "";
				$conn = new MongoClient('mongodb://127.0.0.1');
				$db = $conn->shop;
					$collection = $db->orders;
					$search = $_GET['ordersearch'];
					$js = "function () { var query = '". $search . "'; return this.id == query;}";
					//print $js;
					print '<br/>';
			
				$cursor = $collection->find(array('$where' => $js));
				echo $cursor->count() . ' order(s) found. <br/>';
			
				foreach ($cursor as $obj) {
						echo 'Order ID: ' . $obj['id'] . '<br/>';
						echo 'Name: ' . $obj['name'] . '<br/>';
						echo 'Item: ' . $obj['item'] . '<br/>';
						echo 'Quantity: ' . $obj['quantity']. '<br/>';
						echo '<br/>';
				}
				$conn->close();
			} catch (MongoConnectionException $e) {
				die('Error connecting to MongoDB server : ' . $e->getMessage());
			} catch (MongoException $e) {
				die('Error: ' . $e->getMessage());
			}
		}
		?>


		<b>Use the Order ID to locate your order:</b><br>
		<form method="get" id="usersearch">
			<p>Search <input type="text" name="ordersearch" id="ordersearch" /> <input type="submit" name="submitbutton"
					value="Submit" /></p>
		</form>
		<div id="results">
			<?php echo $result; ?>
		</div>
	</body>

</html>