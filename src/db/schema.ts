import { pgTable, text, serial, timestamp, jsonb, doublePrecision, integer } from 'drizzle-orm/pg-core';
import { relations } from 'drizzle-orm';

// Users table authenticated via Firebase Auth
export const users = pgTable('users', {
  id: serial('id').primaryKey(),
  uid: text('uid').notNull().unique(), // Firebase Auth UID
  email: text('email').notNull(),
  displayName: text('display_name'),
  photoUrl: text('photo_url'),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});

// Enterprise Profiles table
export const profiles = pgTable('profiles', {
  id: text('id').primaryKey(),
  userId: text('user_id'), // Optional owner Firebase UID
  companyName: text('company_name').notNull(),
  industry: text('industry'),
  scale: text('scale'),
  market: text('market'),
  registrationStatus: text('registration_status'),
  confidenceScore: doublePrecision('confidence_score').default(95.0),
  summary: text('summary'),
  website: text('website'),
  location: text('location'),
  categoryIcon: text('category_icon'),
  inputs: jsonb('inputs'),
  products: jsonb('products'),
  registrationDetails: jsonb('registration_details'),
  marketShare: integer('market_share').default(75),
  metrics: jsonb('metrics'),
  feed: jsonb('feed'),
  createdAt: timestamp('created_at').defaultNow(),
  updatedAt: timestamp('updated_at').defaultNow(),
});

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  profiles: many(profiles),
}));

export const profilesRelations = relations(profiles, ({ one }) => ({
  user: one(users, {
    fields: [profiles.userId],
    references: [users.uid],
  }),
}));
