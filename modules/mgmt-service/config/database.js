const { Sequelize } = require('sequelize');

async function getDatabaseConfig() {
  return {
    host: 'mgmt-db',
    port: 3306,
    username: 'username',
    password: 'password',
    database: 'database',
    dialect: 'mariadb'
  };
}

async function initializeDatabase() {
  const config = await getDatabaseConfig();
  const sequelize = new Sequelize(config.database, config.username, config.password, {
    host: config.host,
    port: config.port,
    dialect: config.dialect
  });

  return sequelize;
}

module.exports = initializeDatabase;