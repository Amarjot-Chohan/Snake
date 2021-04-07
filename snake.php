<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>snake</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <style>
        body {
            background-image: url("clouds.jpeg");
            opacity: 0.5;
            padding: 50px;
        }
        table {
            color: black;
        }
    </style>
</head>
<body>
    <h1>Leader Board</h1>
    <br>
    <div>
    <table style="width: auto;" class="table" >
        <tr><th>Rank</th><th>Username</th><th>Score</th><th>Date</th></tr>
<?php
    $host = "localhost";
    $dbusername = "root"; // username
    $dbpassword = ""; // your password
    $dbname = "test";  // dbname

    //Create connection
    $conn = new mysqli($host, $dbusername, $dbpassword, $dbname);

    $sql = "SELECT * FROM leaderboard ORDER BY Score DESC";
    $result = mysqli_query($conn, $sql);
    $resultCheck = mysqli_num_rows($result);
    $counter = 0;

    if ($resultCheck > 0) {

        while($row = mysqli_fetch_assoc($result))
        {
           $counter++;
           echo '<tr><td>'.$counter.'</td>';
           echo '<td>'.$row['Username'].'</td>';
           echo '<td>'.$row['Score'].'</td>';
           echo '<td>'.$row['Date'].'</td></tr>';
        }
    } else {
            echo "Fail";
    }

?>
    </table>
    <div>
</body>
</html>