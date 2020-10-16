const path = require('path')
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const nodeExternals = require('webpack-node-externals');

const config = {
  mode: 'development',
  entry: './src/main.js',
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js' // 'vue/dist/vue.common.js' for webpack 1
    }
  },
  output: {
    path: path.resolve(__dirname, 'static/frontend'),
    filename: 'main.js'
  },
  module: {
    rules: [
      // ... other rules
      {
        test: /\.vue$/,
        loader: 'vue-loader'
      },
	  {
        test: /\.js$/,
		    exclude: /node_modules/,
        loader: 'babel-loader'
      },
	  {
        test: /\.css$/,
		    use: [
          'vue-style-loader',
          'style-loader',
          'css-loader'
        ]
      },
	  {
        test: /\.(png|jpe?g|gif)$/i,
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