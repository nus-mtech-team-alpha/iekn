const { DataTypes } = require('sequelize');
const initializeDatabase = require('../config/database');
const defineRoleModel = require('./Role');

async function defineUserModel() {
  const sequelize = await initializeDatabase();
  const Role = await defineRoleModel();

  const User = sequelize.define('User', {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false
    },
    email: {
      type: DataTypes.STRING,
      allowNull: false,
      unique: true
    },
    password: {
      type: DataTypes.STRING,
      allowNull: false
    }
  });

  User.belongsTo(Role, { foreignKey: 'roleId' });

  return User;
}

module.exports = defineUserModel;