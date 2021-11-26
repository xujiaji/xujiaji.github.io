---
title: 贷款计算器公式
date: 2021-11-24 15:33:32
categories:
  - 数学
tags:
	- 贷款
---

## 等额本息贷款计算
> 每月还款额

$$每月还款额 = {贷款本金 \times 月利率 \times (1 + 月利率)^{还款月数} \over (1 + 月利率)^{还款月数} - 1}$$

```
每月还款额 = 贷款本金 * (月利率 * (1 + 月利率)^还款月数) / ((1+月利率)^还款月数 - 1)
```

> 还款总额

$$还款总额 = 还款月数 \times 每月还款额$$

> 总利息

$$总利息 = 还款总额 - 贷款本金$$

::: collapse 等额本息公式推导
$贷款本金为\mathrm{A}，银行月利率为	\beta，还款月数n，设月还款额为x，排列出从1月到n月，每月所欠银行贷款$

$\begin{align} 第1月欠款 & = \mathrm{A} \times (1 + \beta) - x \\ \end{align}$

$\begin{align} 第2月欠款 & = (\mathrm{A} \times (1 + \beta) - x) \times (1 + \beta) - x \\ & = \mathrm{A} \times (1 + \beta) \times (1 + \beta) - x \times (1 + \beta) - x  \\ & = \mathrm{A} \times (1 + \beta)^2 - x \times (1 + (1 + \beta)) \end{align}$

$\begin{align} 第3月欠款 & = (\mathrm{A} \times (1 + \beta)^2 - x \times (1 + (1 + \beta))) \times (1 + \beta) - x \\ & = \mathrm{A} \times (1 + \beta)^3 - x \times (1 + (1 + \beta)) \times (1 + \beta) - x \\ & = \mathrm{A} \times (1 + \beta)^3 - x \times ((1 + \beta) + (1 + \beta)^2) - x \\ & = \mathrm{A} \times (1 + \beta)^3 - x \times (1 + (1 + \beta) + (1 + \beta)^2) \\ \end{align}$

$\begin{align} 第n月欠款 & = \mathrm{A} \times (1 + \beta)^n - x \times (1 + (1 + \beta) + (1 + \beta)^2 + ... + (1 + \beta)^(n - 1)) \\ & = \mathrm{A} \times (1 + \beta)^n - x \times {((1 + \beta)^n - 1) \over \beta} \end{align}$

[幂之和公式换算参考点这里：M^1 + M^2 + M^3 + ... + M^n的求和公式](https://blog.xujiaji.com/post/math-M-1-M-2-M-3-M-n)

$\begin{align} & \because 第n月刚好还完银行所有贷款 \\ & \therefore \mathrm{A} \times (1 + \beta)^n - x \times {((1 + \beta)^n - 1) \over \beta} = 0 \\ & \therefore x \times {((1 + \beta)^n - 1) \over \beta} = \mathrm{A} \times (1 + \beta)^n \\ & \therefore x = \mathrm{A} \times (1 + \beta)^n \times {\beta \over ((1 + \beta)^n - 1)} \\ & \therefore x = {\mathrm{A} \times \beta \times (1 + \beta)^n \over ((1 + \beta)^n - 1)} \end{align}$

:::

## 等额本金计算
> 每月还款本金

$$每月还款本金 = {贷款本金 \over 还款月数}$$

> 每月还款额

$$每月还款额 = 每月还款本金 + (贷款本金 - 已还本金) \times 月利率$$

> 总利息

$$总利息 = {{贷款本金 \times 月利率 \times (还款月数 + 1)} \over 2}$$

::: collapse 等额本金总利息公式推导
$贷款本金为\mathrm{A}，银行月利率为 \beta，还款月数n，每月利息为当月剩余本金乘以月利息，因此他们之和可表现为：$

$\begin{align} & (\mathrm{A} - 0 \times {\mathrm{A} \over n}) \times \beta + (\mathrm{A} - 1 \times {\mathrm{A} \over n}) \times \beta + (\mathrm{A} - 2 \times {\mathrm{A} \over n}) \times \beta + ... + (\mathrm{A} - (n - 1) \times {\mathrm{A} \over n}) \times \beta \\ &= ((\mathrm{A} - 0) + (\mathrm{A} - 1 \times {\mathrm{A} \over n}) + (\mathrm{A} - 2 \times {\mathrm{A} \over n}) + ... + (\mathrm{A} - (n - 1) \times {\mathrm{A} \over n})) \times \beta \\ &= 1 + (1 - {1 \over n}) + (1 - {2 \over n})) + ... + (1 - {(n - 1) \over n})) \times \beta \times \mathrm{A} \\ &= ({n \over n} + {(n - 1) \over n} + {(n - 2) \over n} + ... + {1 \over n}) \times \beta \times \mathrm{A} \\  &= (n + (n - 1) + (n - 2) + ... + 1) \times {{\beta \times \mathrm{A}} \over n} \\ &= {{n \times (n + 1)} \over 2} \times {{\beta \times \mathrm{A}} \over n} \\ &= {{\beta \times \mathrm{A} \times (n + 1)} \over 2} \end{align}$

:::