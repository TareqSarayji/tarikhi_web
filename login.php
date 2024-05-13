    <?php

    $servername = "localhost";
    $dbUsername = "root";
    $password = "root";
    $dbname = "tarikhi";

    // Create connection
    $conn = new mysqli($servername, $dbUsername, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    session_start();

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $username = $_POST['username'];
        $password = $_POST['passkey'];  // This should match the 'name' attribute of your password input in the HTML form

        // Prepare a select statement
        $query = $conn->prepare("SELECT username, passkey FROM `tarikhi-db` WHERE username = ?");
        $query->bind_param("s", $username);

        if ($query->execute()) {
            $result = $query->get_result();

            if ($result->num_rows === 1) {
                $user = $result->fetch_assoc();

                // Use password_verify to check the entered password against the hashed password from the database
                if (password_verify($password, $user['passkey'])) {
                    $_SESSION['loggedin'] = true;
                    $_SESSION['username'] = $user['username'];

                    // Redirect to Main Webpage.html
                    header("Location: Main Webpage.html");
                    exit; // Make sure no further code is executed after redirection

                } else {
                    echo "Password is incorrect.";
                }
            } else {
                echo "Username not found.";
            }
        } else {
            echo "Error: " . $query->error;
        }

        $query->close();
    }

    $conn->close();
    ?>
