module.exports = {
    'env': {
        'browser': true,
        'es2021': true
    },
    'extends': [
        'eslint:recommended',
        'plugin:vue/vue3-essential',
        'plugin:vue/vue3-recommended',
        'prettier',
        '@vue/eslint-config-typescript'
    ],
    'overrides': [
        {
            'env': {
                'node': true
            },
            'files': [
                '.eslintrc.{vue,js,cjs}'
            ],
            'parserOptions': {
                'sourceType': 'script'
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
            },
            'rules': {
                'vue/multi-word-component-names': 0,
                'vue/no-reserved-component-names': 0,
                'vue/first-attribute-linebreak': 0,
<<<<<<< HEAD
=======
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
            }
        }
    ],
    'parserOptions': {
        'ecmaVersion': 'latest',
        'sourceType': 'module'
    },
    'plugins': [
        'vue',
<<<<<<< HEAD
<<<<<<< HEAD
    ],
    'rules': {
        'quotes': [2, 'single', { 'avoidEscape': true }],
        'vue/multi-word-component-names': 0,
        'vue/no-reserved-component-names': 0,
        'vue/first-attribute-linebreak': 0,
=======
        '@typescript-eslint'
=======
>>>>>>> d6d6125 (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
    ],
    'rules': {
<<<<<<< HEAD
        'quotes': [2, 'single', { 'avoidEscape': true }]
>>>>>>> 1b0447f (Feature: ID-hGqw1FNt: addition of UI components & Chevron diagram and switch to ECharts)
=======
        'quotes': [2, 'single', { 'avoidEscape': true }],
        'vue/multi-word-component-names': 0,
        'vue/no-reserved-component-names': 0,
        'vue/first-attribute-linebreak': 0,
>>>>>>> 8da3a2a (Add BaseChart, fix Chevron to one big diagram, convert to typescript)
    }
}
