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
            },
            'rules': {
                'vue/multi-word-component-names': 0,
                'vue/no-reserved-component-names': 0,
                'vue/first-attribute-linebreak': 0,
            }
        }
    ],
    'parserOptions': {
        'ecmaVersion': 'latest',
        'sourceType': 'module'
    },
    'plugins': [
        'vue',
    ],
    'rules': {
        'quotes': [2, 'single', { 'avoidEscape': true }],
        'vue/multi-word-component-names': 0,
        'vue/no-reserved-component-names': 0,
        'vue/first-attribute-linebreak': 0,
    }
}
