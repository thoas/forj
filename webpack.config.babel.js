const path = require('path')
const webpack = require('webpack')

const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CopyPlugin = require('copy-webpack-plugin')
const cssnano = require('cssnano')

const baseDir = path.resolve(__dirname, 'src/forj/static/site')
const buildDir = path.resolve(baseDir, 'build')

module.exports = {
  mode: process.env.NODE_ENV || 'development',
  context: `${baseDir}/src`,
  entry: {
    editor: ['./javascript/editor.js'],
    collection: ['./javascript/collection.js', './javascript/base.js'],
    home: ['./stylesheet/styles.js', './javascript/index.js', './javascript/base.js'],
    checkout: ['./javascript/forms.js', './javascript/checkout.js'],
    payment: ['./javascript/forms.js', './javascript/payment.js'],
    styles: ['./javascript/styles.js']
  },
  output: {
    path: `${baseDir}/build`,
    filename: 'javascript/[name].js',
    publicPath: '../'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader'
      },
      {
        test: /\.(eot|svg|ttf|ico|json|bin|woff|woff2|otf|png|gif|jpg)$/,
        loader: 'file-loader?name=[path][name].[ext]',
        include: [`${baseDir}/src/assets`, `${baseDir}/src/shaders`]
      },
      {
        test: /\.(sass|scss)$/,
        use: [
          'style-loader',
          {
            loader: MiniCssExtractPlugin.loader
          },
          'css-loader',
          'postcss-loader',
          'sass-loader'
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'stylesheet/main.css',
      chunkFilename: '[id].css'
    }),
    new OptimizeCssAssetsPlugin({
      assetNameRegExp: /\.css$/g,
      cssProcessor: cssnano,
      cssProcessorOptions: { discardComments: { removeAll: true } },
      canPrint: true
    }),
    new CopyPlugin([
      {
        from: '*.html',
        to: buildDir
      }
    ])
  ]
}
