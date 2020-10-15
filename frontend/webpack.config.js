const path = require('path')
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const nodeExternals = require('webpack-node-externals');

const config = {
  mode: 'development',
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, 'static/frontend'),
    filename: 'main.js'
  },
  module: {
    rules: [
      // ... other rules
      {
        test: /\.vue$/,
		exclude: /node_modules/,
        loader: 'vue-loader'
      },
	  {
        test: /\.js$/,
		exclude: /node_modules/,
        loader: 'babel-loader'
      },
	  {
        test: /\.css$/,
		exclude: /node_modules/,
        use: [
          'vue-style-loader',
          'css-loader'
        ]
      },
	  {
        test: /\.(png|jpe?g|gif)$/i,
		exclude: /node_modules/,
        use: [
          {
            loader: 'file-loader',
          },
        ],
      },
    ]
  },
  plugins: [
    // make sure to include the plugin!
    new VueLoaderPlugin()
  ]
}
module.exports = config