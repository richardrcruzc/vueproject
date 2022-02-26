var gulp 		= require('gulp'),
	sass 		= require('gulp-sass'),
    minifyHTML  = require('gulp-minify-html'),
	uglify  	= require('gulp-uglify'),
	rename 		= require('gulp-rename'),
	minifyCss 	= require('gulp-minify-css'),
	del 		= require('del'),
	browserSync = require('browser-sync'),
	imagemin 	= require('gulp-imagemin'),
	shell       = require('gulp-shell');


var srcDir = './src/',
    distDir = './static/',
    templateDir = './web/jinja2/arc';

var path = {
	css: {
		src: srcDir + 'assets/sass/**/*.scss',
		vendors: srcDir + 'vendors/css/*.css',
		dest: distDir + 'css',
	},
	js: {
		src: srcDir + 'assets/js/**/*.js',
		vendors: srcDir + 'vendors/js/**/*.js',
		dest: distDir + 'js',
	},
	vue: {
		src: srcDir + 'component/**/*.vue',
		dest: distDir + 'js',
	},
	img: {
		src: srcDir + 'assets/img/**/*',
		dest: distDir + 'img',
	},
	font: {
		src: srcDir + 'assets/fonts/**/*',
		dest: distDir + 'fonts',
	},
	html: {
		src: [srcDir + 'html/**/*.html'],
		dest: templateDir,
	},
};

gulp.task('clean:all', function(cb) {
	//del(['app/static'], cb);
	//del(['app/jinja2'], cb);
});

gulp.task('clean:build', function(cb) {
	//del(['app/static'], cb);
	//del(['app/jinja2'], cb);
});

gulp.task('css', function() {
	return gulp.src(path.css.src)
		.pipe(sass({
			style: 'compressed',
			includePaths: [
				path.css.src
			]
		}).on('error', sass.logError))
		//.pipe(minifyCss({compatibility: 'ie8'}))
		.pipe(gulp.dest(path.css.dest));
		//.pipe(browserSync.stream());
});

gulp.task('img', function() {
	return gulp.src(path.img.src)
		.pipe(gulp.dest(path.img.dest));
});

gulp.task('fonts', function() {
	return gulp.src([path.font.fontawesome, path.font.src])
		.pipe(gulp.dest(path.font.dest));
});

gulp.task('html', function() {
    return gulp.src(path.html.src)
	    //.pipe(minifyHTML())
		.pipe(gulp.dest(path.html.dest));
		//.pipe(browserSync.stream());
});

gulp.task('js', function() {
	return gulp.src(path.js.src)
		//.pipe(uglify())
		.pipe(gulp.dest(path.js.dest));
		//.pipe(browserSync.stream());
});

gulp.task('build:vendors:css', function() {
	return gulp.src(path.css.vendors)
		.pipe(minifyCss({compatibility: 'ie8'}))
		.pipe(gulp.dest(path.css.dest));
		//.pipe(browserSync.stream());
});

gulp.task('build:vendors:js', function() {
	return gulp.src(path.js.vendors)
		.pipe(uglify())
		.pipe(gulp.dest(path.js.dest));
		//.pipe(browserSync.stream());
});

/*
gulp.task('image', function() {
    gulp.src(paths.image.source)
        .pipe(imagemin())
        .on('error', function(err) {
            displayError(err);
        })
        .pipe(gulp.dest(paths.image.dest))
        .pipe(browserSync.reload({
            stream: true
        }));
});
*/

gulp.task('setup', ['build:vendors:css', 'build:vendors:js', 'fa']);

gulp.task('watch', function() {
	gulp.watch(path.css.src, ['css']);
	gulp.watch(path.js.src, ['js']);
	gulp.watch(path.img.src, ['img']);
	gulp.watch(path.html.src, ['html']);
});

//gulp.task('default', ['css', 'js', 'img', 'fonts', 'html', 'watch']);
gulp.task('default', ['css', 'html', 'js', 'img', 'watch']);