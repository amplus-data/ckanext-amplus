var gulp = require('gulp');
var sass = require('sass')(require('sass'));
var autoprefixer = require('gulp-autoprefixer');
// var sourcemaps = require('gulp-sourcemaps'); - Uncomment when developing

// Rebuild CSS from sass
gulp.task('sass', function () {
  return gulp.src('sass/custom.scss')
    // .pipe(sourcemaps.init()) - Uncomment when developing
    .pipe(sass())
    .pipe(autoprefixer({
      browsers: [
        "last 5 versions",
        "ie >= 11"
      ]
    }))
    // .pipe(sourcemaps.write()) - Uncomment when developing
    .pipe(gulp.dest('css'));
});

gulp.task('fonts', function() {
  return gulp.src('node_modules/typeface-barlow/files/*')
    .pipe(gulp.dest('../public/base/fonts'))
})

// Watch for sass file changes
gulp.task("watch", function () {
  gulp.watch(["sass/**/*.sass"],
    gulp.parallel("sass"));
});

// The default Gulp.js task
gulp.task('default', gulp.series('sass', 'fonts', 'watch'));
