const { Pool } = require('pg');

const databaseServiceUrl = process.env.DATABASE_SERVICE_URL || 'database-service';

const pool = new Pool({
	user: 'user',
	password: 'password',
	host: databaseServiceUrl,
	port: 5432,
	database: 'mydb',
});

module.exports = {
  query: (text, params) => pool.query(text, params)
};
