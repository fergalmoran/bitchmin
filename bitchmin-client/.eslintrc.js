module.exports = {
    root: true,

    env: {
        node: true
    },

    extends: ['plugin:vue/essential', 'eslint:recommended', '@vue/typescript/recommended'],
    parserOptions: {
        ecmaVersion: 2020
    },
    rules: {
        'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
        quotes: [2, 'single', { avoidEscape: true }],
        '@typescript-eslint/quotes': [2, 'single', { avoidEscape: true }],
        'max-len': [
            'error',
            {
                code: 120
            }
        ],
        indent: [2, 4]
    },
    overrides: [
        {
            files: ['**/__tests__/*.{j,t}s?(x)', '**/tests/unit/**/*.spec.{j,t}s?(x)'],
            env: {
                mocha: true
            }
        },
        {
            files: ['**/__tests__/*.{j,t}s?(x)', '**/tests/unit/**/*.spec.{j,t}s?(x)'],
            env: {
                mocha: true
            }
        }
    ]
};
