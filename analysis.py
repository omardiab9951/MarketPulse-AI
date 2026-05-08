import matplotlib.pyplot as plt

# ============================================
# STUDENT 5: VISUALIZATION LEAD
# ============================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('E-Commerce Funnel Analysis - Electronics (Feb 2020)',
             fontsize=14, fontweight='bold')

# Chart 1: Funnel Bar Chart
axes[0,0].bar(['Views','Carts','Purchases'], [views, carts, purchases],
               color=['#1a2657','#2e4799','#e84545'])
axes[0,0].set_title('Purchase Funnel')
axes[0,0].set_ylabel('Count')
for i, v in enumerate([views, carts, purchases]):
    axes[0,0].text(i, v + 1000, f'{v:,}', ha='center', fontsize=9)

# Chart 2: Top Brands Bar Chart
brand_funnel = df.groupby(['brand','event_type']).size().unstack(fill_value=0)
for col in ['view','cart','purchase']:
    if col not in brand_funnel.columns:
        brand_funnel[col] = 0
brand_funnel['purchase_rate'] = (brand_funnel['purchase'] / brand_funnel['view'] * 100).round(2)
top_brands = brand_funnel[brand_funnel['view'] > 100].sort_values('purchase_rate', ascending=False).head(10)

axes[0,1].barh(top_brands.index, top_brands['purchase_rate'], color='#2e4799')
axes[0,1].set_title('Top 10 Brands - Purchase Rate %')
axes[0,1].set_xlabel('Purchase Rate %')

# Chart 3: Price Groups Bar Chart
price_funnel = df.groupby(['price_group','event_type']).size().unstack(fill_value=0)
for col in ['view','cart','purchase']:
    if col not in price_funnel.columns:
        price_funnel[col] = 0
price_funnel['purchase_rate'] = (price_funnel['purchase'] / price_funnel['view'] * 100).round(2)

axes[1,0].bar(price_funnel.index, price_funnel['purchase_rate'], color='#22c55e')
axes[1,0].set_title('Purchase Rate by Price Group')
axes[1,0].set_xlabel('Price Group')
axes[1,0].set_ylabel('Purchase Rate %')

# Chart 4: Hourly Line Chart
hourly = df.groupby(['hour','event_type']).size().unstack(fill_value=0)
for col in ['view','cart','purchase']:
    if col not in hourly.columns:
        hourly[col] = 0
hourly['conversion_rate'] = (hourly['purchase'] / hourly['view'] * 100).round(2)

axes[1,1].plot(hourly.index, hourly['conversion_rate'], marker='o', color='#e84545')
axes[1,1].set_title('Conversion Rate by Hour of Day')
axes[1,1].set_xlabel('Hour')
axes[1,1].set_ylabel('Conversion Rate %')

plt.tight_layout()
plt.savefig('funnel_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart saved!")