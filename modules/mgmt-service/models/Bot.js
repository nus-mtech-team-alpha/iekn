const { DataTypes } = require('sequelize');
const initializeDatabase = require('../config/database');
const defineUserModel = require('./User');

async function defineBotModel() {
  const sequelize = await initializeDatabase();
  const User = await defineUserModel();

  const Bot = sequelize.define('Bot', {
    id: {
      type: DataTypes.INTEGER,
      autoIncrement: true,
      primaryKey: true
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false
    },
    description: {
      type: DataTypes.STRING,
      allowNull: true
    }
  });

  Bot.belongsTo(User, { foreignKey: 'ownerId' });

  return Bot;
}

module.exports = defineBotModel;