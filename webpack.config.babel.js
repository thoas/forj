import path from 'path';
import webpack from 'webpack';
import ExtractTextPlugin from 'extract-text-webpack-plugin';

const baseDir = path.resolve(__dirname, 'src/forj/static/site');


module.exports = {
  context: `${baseDir}/src`,
  entry: {
    app: [
      './stylesheet/styles.js',
      './javascript/index.js'
    ],
    styles: [
      './javascript/styles.js',
    ],
  },
  output: {
    path: `${baseDir}/build`,
    filename: 'javascript/[name].js',
    publicPath: '../',
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
      },
      {
        test: /\.(eot|svg|ttf|woff|woff2|otf|png|gif|jpg|frag)$/,
        loader: 'file-loader?name=[path][name].[ext]',
        include: [
          `${baseDir}/src/assets`,
          `${baseDir}/src/shaders`,
        ]
      },
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract([
          'css-loader?sourceMap',
          'postcss-loader?sourceMap',
          'sass-loader?sourceMap',
        ]),
      },
    ],
  },
  plugins: [
    new ExtractTextPlugin({
      filename: 'stylesheet/main.css',
      allChunks: true,
    }),
  ],
}