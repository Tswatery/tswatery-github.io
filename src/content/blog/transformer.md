---
title: "Transformer相关问题总结"
date: 2026-08-06
summary: "Transformer架构、注意力机制与KV Cache相关问题总结"
tags: ["Transformer", "深度学习"]
---

## 1 Transformer的整体架构是什么？和RNN、CNN的核心差异在哪？

原始的Transformer是Encoder-Decoder的seq2seq架构，在Encoder阶段采用双向self-attention产生上下文关系信息，Decoder阶段用因果Attention自回归生成答案，并通过cross attention读取Encoder计算过的上下文关系信息。其关键组件有Embedding层以及位置编码、多头注意力层、FFN的非线性变换，每个子层的Attention与FFN之间会有Add和Norm层保证深层可训练。

RNN中下一状态依赖于上一状态，并行性差，且对于长序列的路径长，梯度传播困难，拥有注意力机制的Transformer将任意两个token之间的计算距离缩短至O(1)，可并行训练；CNN通过卷积核获取局部信息，对于长程任务需要多层堆叠，Transformer单层即可全局交互。

但是代价是注意力机制的复杂度是平方级别，优化手段有FlashAttention、稀疏注意力机制等。

### 这三种Attention有什么区别？

Attention的本质计算都是$softmax(\frac{QK^T}{\sqrt{d_k}})V$，核心区别在于QKV的来源以及mask的覆盖。

双向Attention一般用于Encoder阶段，对于句子中间的某个词，它需要同时看前面的以及后面的词才生成带有上下文的信息的词向量。

因果Attention是用于Decoder阶段，它是生成答案的过程，在训练的时候会使用右上三角矩阵来遮盖信息，从而来模型只看前面已经输出的信息不作弊，在推理阶段由于没有未来答案，所以也只能看前面的信息，所以又叫自回归Attention。

Cross Attention也是Decoder阶段，对于下一个token的生成，Decoder需要参考Encoder中整个句子的信息，目的是做信息融合，这里的Q来自于Decoder，K和V均来自Encoder的最终输出。

## 2 Self-Attention中为什么要除以一个分数？

Attention公式是$softmax(\frac{QK^T}{\sqrt{d_k}})V$，其中的qk的方差会随着$d_k$增大而增大，导致softmax logits过大，分布过尖，梯度容易不稳定，除以它是为了把尺度归化到$O(1)$，稳定训练。

## 3 Decoder中的self-attention以及cross-attention的QKV分别从哪来？

Decoder self-attention的QKV均来自于Decoder当前层输入，训练时用causal mask并行计算，推理时用增量生成并配合KV Cache。cross-attention的Q来自Decoder，K和V来自于Encoder的Memory。

## 4 KV Cache的推理复杂度怎么变化：从“总生成长度T”的角度，naive与cache的复杂度分别是什么？显存代价呢？

naive的复杂度是$O(T^2)$，每次查都需要重新计算KV，cache后的复杂度是$O(1)$，显存代价是$O(T^2)$，是采用空间换时间的典型策略。

## 5 训练时mask矩阵长啥样？ 为什么是这样？

$$
\begin{bmatrix}
1 & 0 & 0 &  ... & 0 \\
1 & 1 & 0 &  ... & 0 \\
...\\
1 & 1 & 1 & ... & 1
\end{bmatrix}
$$

训练时候采用右上三角矩阵，每一行代表一次训练，表示第一次能看第一个token，第二次能看第二个token，防止训练看到答案。

##  6 Multi-Head Attention 的维度关系：假设$d=768$,heads=12，单头的 $d_k$通常是多少？为什么要这么设？

一般是$768\div 12=64$，视角变多，除法的目的是为了拼接回去后能够还原。
