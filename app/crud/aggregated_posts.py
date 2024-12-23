from typing import List

from models.aggregated_posts import AggregatedPost
from models.channel import Channel
from models.post import Post
from models.user_channel import UserChannel
from schemas.aggregated_posts import AggregatedPostModel
from sqlalchemy import desc, func  # Added func here
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_top_aggregated_posts_for_user(
    session: AsyncSession,
    user_id: int,
    top_n: int,
    top_k: int,
) -> List[AggregatedPostModel]:
    # Step 1: Get top_n clusters based on the highest importance_score
    top_clusters_query = (
        select(AggregatedPost.cluster_label, Post.title, func.max(AggregatedPost.importance_score).label("max_score"))
        .join(Post, AggregatedPost.post_link == Post.post_link)
        .join(Channel, Post.channel_link == Channel.channel_link)
        .join(UserChannel, Channel.channel_link == UserChannel.channel_link)
        .filter(UserChannel.user_id == user_id)
        .group_by(AggregatedPost.cluster_label, Post.title)
        .order_by(desc("max_score"))
        .limit(top_n)
    )

    cluster_result = await session.execute(top_clusters_query)
    top_clusters = cluster_result.fetchall()
    cluster_ids = [cluster.cluster_label for cluster in top_clusters]

    if not cluster_ids:
        return []

    # Step 2: Get top_k posts for each top cluster
    posts_query = (
        select(
            AggregatedPost.cluster_label,
            Post.title,
            Channel.channel_link,
            AggregatedPost.post_link,
            AggregatedPost.importance_score,
        )
        .join(Post, AggregatedPost.post_link == Post.post_link)
        .join(Channel, Post.channel_link == Channel.channel_link)
        .join(UserChannel, Channel.channel_link == UserChannel.channel_link)
        .filter(UserChannel.user_id == user_id, AggregatedPost.cluster_label.in_(cluster_ids))
        .order_by(AggregatedPost.cluster_label, desc(AggregatedPost.importance_score))
    )

    posts_result = await session.execute(posts_query)
    posts = posts_result.fetchall()

    # Organize posts by cluster
    aggregated = {cluster_id: {"cluster": cluster_id, "title": "", "posts": []} for cluster_id in cluster_ids}

    for cluster_label, title, channel_link, post_link, importance_score in posts:
        if not aggregated[cluster_label]["title"]:
            aggregated[cluster_label]["title"] = title
        if len(aggregated[cluster_label]["posts"]) < top_k:
            aggregated[cluster_label]["posts"].append(
                {"channel_link": channel_link, "post_link": post_link, "importance_score": importance_score}
            )

    aggregated_data = list(aggregated.values())
    return [AggregatedPostModel(**item) for item in aggregated_data]
