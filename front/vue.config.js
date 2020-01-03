const path = require('path');
const fs = require('fs');
const sass = require('sass');
const fibers = require('fibers');
const appConfig = require('config');

module.exports = {
  assetsDir: 'static',
  publicPath: undefined,
  outputDir: path.resolve(__dirname, 'templates'),
  runtimeCompiler: undefined,
  productionSourceMap: undefined,
  parallel: undefined,
  css: undefined,
  chainWebpack: (config) => {
    config.module.rules.delete('sass');

    // add the new one
    config.module.rule('sass')
      .test(/\.s(c|a)ss$/)
      .use('vue-style-loader')
      .loader('vue-style-loader')
      .end()
      .use('css-loader')
      .loader('css-loader')
      .end()
      .use('sass-loader')
      .loader('sass-loader')
      .options({
        implementation: sass,
        sassOptions: {
          fiber: fibers,
          indentedSyntax: true, // optional
        },
      });

    const clientConfigPath = path.resolve(__dirname, 'config/client-config.json');
    fs.writeFileSync(clientConfigPath,
      JSON.stringify(appConfig));
    config.resolve.alias.set('config', clientConfigPath);
  },
};
