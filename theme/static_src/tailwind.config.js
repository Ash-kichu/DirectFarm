/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            colors: {
                primary: 'var(--primary)',
                secondary: 'var(--secondary)',
                green: 'var(--green)',
                brown: 'var(--brown)',
                dark: 'var(--dark)',
                light: 'var(--light)',
            },
            fontFamily: {
                'montserrat' : ['Montserrat', 'serif'],
                'raleway' : ['Raleway', 'serif'],
            },
            boxShadow: {
                'top': '0 10px 20px black',
                'bottom': '0 1px 8px var(--primary)',
            },
            animation: {
                'dropDown': 'dropDown 1s',
                'slideInLeft': 'slideInLeft 1s',
                'slideInRight': 'slideInRight 1s',
                'zoom': 'zoom 1s',
            },
            keyframes: {
                dropDown: {
                    '0%': {
                        opacity:0,
                        transform: 'translateY(-50%)'
                    },
                    '100%': {
                        opacity:1,
                        transform: 'translateY(0)'
                    },
                },
                slideInLeft: {
                    '0%': {
                        opacity:0,
                        transform: 'translateX(50%)'
                    },
                    '100%': {
                        opacity:1,
                        transform: 'translateX(0)'
                    },
                },
                slideInRight: {
                    '0%': {
                        opacity:0,
                        transform: 'translateX(-50%)'
                    },
                    '100%': {
                        opacity:1,
                        transform: 'translateX(0%)'
                    },
                },
                zoom: {
                    '0%': {
                        opacity:0,
                        transform: 'scale(0%)'
                    },
                    '100%': {
                        opacity:1,
                        transform: 'scale(100%)'
                    },
                },
            },

        }
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
