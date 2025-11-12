import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  schema: z.object({
    title: z.string(),
    date: z.date(),
    summary: z.string(),
    tags: z.array(z.string()),
    weather: z.string().optional(),
    mood: z.string().optional(),
    rating: z.number().int().min(1).max(5).optional(),
    updated: z.date().optional(),
    draft: z.boolean().default(false),
    cover: z.object({
      src: z.string(),
      alt: z.string().optional(),
    }).optional(),
    canonicalUrl: z.string().optional(),
  }),
});

export const collections = {
  blog,
};
