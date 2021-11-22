---
title: test_page
date: 2021-11-22 09:32:04
visible: false
---

&nbsp;   | &nbsp;     | &nbsp;
:-------:|:----------:|:-:
One      | Two        | Three


Unordered list
- list item
	+ list item
		* list item
		* list item
			- list item
	+ list item
- list item
	+ list item
	+ list item

Ordered list
1. list item
	1. list item
		1. list item
		2. list item
			1. list item
	2. list item
2. list item
	1. list item
	2. list item

<hr>

- [ ] hahha
- [x] aaaa

{% codeblock %}
alert('Hello World!');
{% endcodeblock %}

{% codeblock Array.map %}
array.map(callback[, thisArg])
{% endcodeblock %}


{% codeblock _.compact http://underscorejs.org/#compact Underscore.js %}
_.compact([0, 1, false, 2, '', 3]);
=> [1, 2, 3]
{% endcodeblock %}

{% gist 59dd307bb56ef7919cc192aa7b547e27 [skill.ts] %}
<script src="https://gist.github.com/ikeq/59dd307bb56ef7919cc192aa7b547e27.js"></script>


stars: <span id="stargazers_count"></span>
<script>
fetch('https://api.github.com/repos/ikeq/hexo-theme-inside')
  .then(res => res.json())
  .then(json => {
    document.getElementById('stargazers_count').innerHTML = json.stargazers_count || json.message;
  });
</script>


::: timeline
- xxx 2020/04/10
- xxx 2020/04/11
- xxx 2020/04/12
- xxx 2020/04/13
:::

::: collapse Click to show a secret
🥱 You got me !
:::

<details>
  <summary>Click to show a secret</summary>
  <p>🥱 You got me !</p>
</details>

# square by default
<!-- ::: tree -->
::: tree icon:arrow
<!-- ::: tree icon:circle -->
- level 1
  - level 2
    - level 3
:::

npm un hexo-renderer-marked --save
npm i hexo-renderer-markdown-it --save
npm install markdown-it-footnote --save
Here is a footnote reference,[^1] and another.[^longnote]

Here is an inline note.^[Inlines notes are easier to write, since
you don't have to pick an identifier and move down to type the
note.]

# MathJax

https://blog.oniuo.com/post/math-jax-ssr-example

When \(a \ne 0\), there are two solutions to \(ax^2 + bx + c = 0\) and they are

\[x = {-b \pm \sqrt{b^2-4ac} \over 2a}.\]


[^1]: Here is the footnote.

[^longnote]: Here's one with multiple blocks.

