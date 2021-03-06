var gulp = require('gulp');
var source = require('vinyl-source-stream');
var buffer = require('vinyl-buffer');
var browserify = require('browserify');
var watchify = require('watchify');
var reactify = require('reactify');
var uglify = require('gulp-uglify');
var gulpif = require('gulp-if');
var derequire = require('gulp-derequire');
var rename = require('gulp-rename');
var argv = require('minimist')(process.argv.slice(2));
var dispatch = require('./dist/dispatch.js');

var path = {
  DEST: 'dist',
  SRC: './src/',
};

var file, dev;
file = typeof argv.i === 'undefined' ? 'article' : argv.i;
dev = typeof argv.d === 'undefined' ? false : true;

var reactTask = function(obj){
    return obj.transform({ global: true }, reactify)
    .bundle()
    .pipe(source(file + '.js'))
    .pipe(derequire())
    .pipe(gulpif(!dev, buffer()))
    .pipe(gulpif(!dev, uglify()))
    .pipe(rename(file + '-' + dispatch.version + '.js'))
    .pipe(gulp.dest(path.DEST));
}

gulp.task('watch', function() {
  var watcher  = watchify(browserify({
    entries: [path.SRC + file + '.js'],
    debug: true,
    cache: {}, packageCache: {}, fullPaths: true
  }));

  return reactTask(watcher.on('update', function () {
      reactTask(watcher);
      console.log('updated');
  }));

});

gulp.task('default', ['watch']);