<?php

// connect
$m = new MongoClient();

// select a database
$db = $m->shop;

// Drop the database
$response = $db->drop();
//print_r($response);

// select a collection (analogous to a relational database's table)
$collection = $db->orders;

// add records
$obj = array( "id"=>"1234","name"=>"Russell","item"=>"ManCity Jersey","quantity"=>"2");
$collection->insert($obj);
$obj = array( "id"=>"42","name"=>"Adrien","item"=>"Fuzzy pink towel","quantity"=>"1");
$collection->insert($obj);
$obj = array( "id"=>"99","name"=>"Justin","item"=>"Bird supplies","quantity"=>"4");
$collection->insert($obj);
$obj = array( "id"=>"1","name"=>"Robin","item"=>"Music gift cards","quantity"=>"100");
$collection->insert($obj);
$obj = array( "id"=>"1001","name"=>"Moses","item"=>"Miami Heat tickets","quantity"=>"1000");
$collection->insert($obj);
$obj = array( "id"=>"66","name"=>"Rick","item"=>"Black hoodie","quantity"=>"1");
$collection->insert($obj);
$obj = array( "id"=>"0","name"=>"Nobody","item"=>"Nothing","quantity"=>"0");
$collection->insert($obj);

// find everything in the collection
$cursor = $collection->find();

// iterate through the results
foreach ($cursor as $obj) {
    echo $obj["name"] . "<br>";
}

// select a database
$db = $m->customers;

// Drop the database
$response = $db->drop();
//print_r($response);

// select a collection (analogous to a relational database's table)
$collection = $db->paymentinfo;

$obj = array( "name"=>"Russell","id"=>"1000","cc"=>"0000000000000000","cvv2"=>"0000");
$collection->insert($obj);
$obj = array( "name"=>"Adrien","id"=>"42","cc"=>"5555123456789999","cvv2"=>"1234");
$collection->insert($obj);
$obj = array( "name"=>"Justin","id"=>"99","cc"=>"5555123456780000","cvv2"=>"4321");
$collection->insert($obj);
$obj = array( "name"=>"Robin","id"=>"1","cc"=>"3333444455556666","cvv2"=>"2222");
$collection->insert($obj);
$obj = array( "name"=>"Moses","id"=>"2","cc"=>"4444555566667777","cvv2"=>"3333");
$collection->insert($obj);
$obj = array( "name"=>"Rick","id"=>"3","cc"=>"5555666677778888","cvv2"=>"5678");
$collection->insert($obj);
$obj = array( "name"=>"Nobody","id"=>"0","cc"=>"4500987654321555","cvv2"=>"9999");
$collection->insert($obj);

// find everything in the collection
$cursor = $collection->find();

// iterate through the results
foreach ($cursor as $obj) {
    echo $obj["cc"] . "<br>";
}


// select a database
$db = $m->appUserData;

// Drop the database
$response = $db->drop();
//print_r($response);

// select a collection (analogous to a relational database's table)
$collection = $db->users;

$obj = array( "name"=>"Russell","username"=>"tcstoolHax0r","email"=>"nosqlmap@sec642.org");
$collection->insert($obj);
$obj = array( "name"=>"Adrien","username"=>"adrien","email"=>"adrien@sec642.org");
$collection->insert($obj);
$obj = array( "name"=>"Justin","username"=>"justin","email"=>"justin@sec642.org");
$collection->insert($obj);
$obj = array( "name"=>"Robin","username"=>"digininja","email"=>"digininja@sec642.org");
$collection->insert($obj);
$obj = array( "name"=>"Moses","username"=>"adrien","email"=>"moses@sec642.org");
$collection->insert($obj);
$obj = array( "name"=>"Rick","username"=>"rick","email"=>"rick@sec642.org");
$collection->insert($obj);
$obj = array( "name"=>"Nobody","username"=>"administrator","email"=>"root@sec642.org");
$collection->insert($obj);

// find everything in the collection
$cursor = $collection->find();

// iterate through the results
foreach ($cursor as $obj) {
    echo $obj["email"] . "<br>";
}

?>