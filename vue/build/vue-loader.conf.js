var utils = require('./utils')
var config = require('../config')
var isProduction = process.env.NODE_ENV === 'production'

var loaders_obj = utils.cssLoaders({
      sourceMap: isProduction
        ? config.build.productionSourceMap
        : config.dev.cssSourceMap,
      extract: isProduction
});

loaders_obj.i18n = '@kazupon/vue-i18n-loader'

module.exports = {
  loaders: loaders_obj,
  transformToRequire: {
    video: 'src',
    source: 'src',
    img: 'src',
    image: 'xlink:href'
  },
  preLoaders: {
    i18n: 'yaml-loader'
  },
}
