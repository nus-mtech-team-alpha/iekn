const { DataTypes } = require('sequelize');
const initializeDatabase = require('../config/database');

async function defineRoleModel() {
  const sequelize = await initializeDatabase();

  const Role = sequelize.define('Role', {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false
    }
  });

  return Role;
}

module.exports = defineRoleModel;