import { db } from './index.ts';
import { profiles } from './schema.ts';
import { eq, desc } from 'drizzle-orm';

export async function getAllProfiles(userId?: string) {
  try {
    if (userId) {
      return await db.select().from(profiles).where(eq(profiles.userId, userId)).orderBy(desc(profiles.createdAt));
    }
    return await db.select().from(profiles).orderBy(desc(profiles.createdAt));
  } catch (error) {
    console.error("Database getAllProfiles failed:", error);
    throw new Error("Database query failed.", { cause: error });
  }
}

export async function getProfileById(id: string) {
  try {
    const res = await db.select().from(profiles).where(eq(profiles.id, id));
    return res[0] || null;
  } catch (error) {
    console.error("Database getProfileById failed:", error);
    throw new Error("Database query failed.", { cause: error });
  }
}

export async function saveProfile(profileData: any) {
  try {
    const existing = await getProfileById(profileData.id);
    if (existing) {
      const updated = await db.update(profiles)
        .set({
          companyName: profileData.companyName,
          industry: profileData.industry,
          scale: profileData.scale,
          market: profileData.market,
          registrationStatus: profileData.registrationStatus,
          confidenceScore: profileData.confidenceScore,
          summary: profileData.summary,
          website: profileData.website,
          location: profileData.location,
          categoryIcon: profileData.categoryIcon,
          inputs: profileData.inputs,
          products: profileData.products,
          registrationDetails: profileData.registrationDetails,
          locations: profileData.locations,
          marketShare: profileData.marketShare,
          metrics: profileData.metrics,
          feed: profileData.feed,
          updatedAt: new Date(),
        })
        .where(eq(profiles.id, profileData.id))
        .returning();
      return updated[0];
    } else {
      const inserted = await db.insert(profiles)
        .values({
          id: profileData.id,
          userId: profileData.userId || null,
          companyName: profileData.companyName,
          industry: profileData.industry,
          scale: profileData.scale,
          market: profileData.market,
          registrationStatus: profileData.registrationStatus,
          confidenceScore: profileData.confidenceScore,
          summary: profileData.summary,
          website: profileData.website,
          location: profileData.location,
          categoryIcon: profileData.categoryIcon,
          inputs: profileData.inputs,
          products: profileData.products,
          registrationDetails: profileData.registrationDetails,
          locations: profileData.locations,
          marketShare: profileData.marketShare,
          metrics: profileData.metrics,
          feed: profileData.feed,
          createdAt: profileData.createdAt ? new Date(profileData.createdAt) : new Date(),
          updatedAt: new Date(),
        })
        .returning();
      return inserted[0];
    }
  } catch (error) {
    console.error("Database saveProfile failed:", error);
    throw new Error("Database save operation failed.", { cause: error });
  }
}

export async function deleteProfileById(id: string) {
  try {
    await db.delete(profiles).where(eq(profiles.id, id));
    return true;
  } catch (error) {
    console.error("Database deleteProfileById failed:", error);
    throw new Error("Database delete operation failed.", { cause: error });
  }
}
