const express = require("express");
const mysql = require("mysql2");
const app = express();
const bodyParser = require("body-parser");
const port = 4676;


const connection = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "database101",
  });

app.use(bodyParser.json({limit: "50mb"}));

// CREATE(insert)
app.post("/tolongges", (req, res) => {
    const { datetime,image } = req.body;
  
    connection.query(
      "INSERT INTO detection (datetime,image) VALUES (?,?)",
      [datetime,image],
      (err, results) => {
        try {
          if (results.affectedRows > 0) {
            res.json({ message: "Data has been added!" });
          } else {
            res.json({ message: "Something went wrong." });
          }
        } catch (err) {
          res.json({ message: err });
        }
      }
    );
  });


app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});