module.exports = {
  transpileDependencies: [
    'vuetify'
  ],
  pluginOptions: {
    'style-resources-loader': {
      preProcessor: 'scss',
      patterns: []
    }
  },
  configureWebpack: {
    devtool: 'source-map'
  }
};
