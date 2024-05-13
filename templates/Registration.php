<?php

$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "tarikhi";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['register'])) {

    $username = preg_replace("/[^a-zA-Z]/", "", $_POST['username']); // Constraint: Only accept alphabet values for username
    $firstname = $_POST['firstname']; 
    $lastname = $_POST['lastname']; 
    $password = $_POST['passkey'];
    // Hash the password before storing it in the database
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Prepare an insert query with parameters
    $insert_query = $conn->prepare("INSERT INTO `tarikhi-db` (username, firstname, lastname, passkey) VALUES (?, ?, ?, ?)");
    if (!$insert_query) {
        die("Error preparing statement: " . $conn->error);
    }

    $bind_result = $insert_query->bind_param("ssss", $username, $firstname, $lastname, $hashed_password);
    if (!$bind_result) {
        die("Error binding parameters: " . $insert_query->error);
    }

    // Execute the prepared statement and check for success
    if ($insert_query->execute()) {
        echo "User registered successfully";
    } else {
        echo "Error executing statement: " . $insert_query->error;
    }

    // Close the prepared statement
    $insert_query->close();
} else {
    echo "No data received from the form.";
}

// Close database connection
$conn->close();
?>
