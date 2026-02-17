import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import prettier from 'eslint-config-prettier';
import svelteParser from 'svelte-eslint-parser';

/** @type {import('eslint').Linter.Config[]} */
export default [
	{
		languageOptions: {
			globals: {
				...globals.browser,
				...globals.node
			}
		}
	},
	...svelte.configs['flat/recommended'],
	{
		files: ['**/*.svelte'],
		languageOptions: {
			parser: svelteParser,
			parserOptions: {
				extraFileExtensions: ['.svelte']
			}
		}
	},
	prettier,
	{
		rules: {
			'svelte/no-at-html-tags': 'off',
			'svelte/require-each-key': 'warn',
			'svelte/no-navigation-without-resolve': 'off'
		}
	},
	{
		ignores: ['build/', '.svelte-kit/', 'dist/', 'node_modules/']
	}
];
