const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const app = express();
const port = 5001;

app.use(cors());

const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '12345678',
    database: 'north_america'
});

const s_db = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: '12345678',
  database: 'south_america'
});

db.connect((err) => {
    if (err) throw err;
    console.log('Connected to MySQL database!');
});

s_db.connect((err) => {
  if (err) throw err;
  console.log('Connected to MySQL database!');
});

app.get('/api/north_america/logo', (req, res) => {
    db.query('SELECT name, logo_url FROM logo', (err, results) => {
        if (err) throw err;
        res.json(results);
    });
});

app.get('/api/north_america/flag', (req, res) => {
    db.query('SELECT flag_url FROM flag', (err, results) => {
        if (err) throw err;
        res.json(results);
    });
});


app.get('/api/north_america/brand/:file_name', (req, res) => {
  const brandName = req.params.name;

  // Query the database for brand details based on the brand name
  db.query(
      'SELECT file_name, model_name,image_url,type,engine-type FROM na_brands WHERE file_name = ?', 
      [brandName], 
      (err, results) => {
          if (err) throw err;

          // Check if brand is found
          if (results.length > 0) {
              // Assuming you also want to fetch models as an array of model names
              db.query(
                  'SELECT file_name FROM car_models WHERE brand_name = ?', 
                  [brandName],
                  (err, modelResults) => {
                      if (err) throw err;

                      // Add models to the brand details
                      const brandDetails = {
                          file_name: results[0].file_name,
                          model_name: results[0].model_name,
                          image_url: results[0].image_url,
                          type: results[0].type,
                          engine_type: results[0].engine_type,
                          models: modelResults.map(model => model.name), // List of models
                      };

                      res.json(brandDetails);
                  }
              );
          } else {
              res.status(404).json({ error: 'Brand not found' });
          }
      }
  );
});

app.get('/api/south_america/flag', (req, res) => {
  s_db.query('SELECT flag_url FROM flags', (err, results) => {
      if (err) throw err;
      res.json(results);
  });
});

app.get('/api/south_america/logo', (req, res) => {
  s_db.query('SELECT name, logo_url FROM logo', (err, results) => {
      if (err) throw err;
      res.json(results);
  });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
