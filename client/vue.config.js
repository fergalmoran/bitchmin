module.exports = {
    pluginOptions: {
        'style-resources-loader': {
            preProcessor: 'scss',
            patterns: [],
        },
    },
    configureWebpack: {
        devtool: 'source-map',
    },
    transpileDependencies: ['vuetify'],
};
