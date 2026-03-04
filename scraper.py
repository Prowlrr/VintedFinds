import 'package:flutter/material.dart';

void main() {
  runApp(const VintedLuxuryApp());
}

class VintedLuxuryApp extends StatelessWidget {
  const VintedLuxuryApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vinted Discord Monitor',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF00C2C2), // Vinted Brand Cyan
          surface: const Color(0xFF121212),
        ),
        cardTheme: CardTheme(
          color: const Color(0xFF1E1E1E),
          elevation: 5,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        ),
      ),
      home: const DashboardScreen(),
    );
  }
}

// --- DATA STRUCTURE ---

class ClothingPiece {
  final String id;
  final String brand;
  final String name;
  final double price;
  final double estimatedResell;
  final String imageUrl;
  final String discordChannel;
  final DateTime foundAt;
  final bool isImportant;

  ClothingPiece({
    required this.id,
    required this.brand,
    required this.name,
    required this.price,
    required this.estimatedResell,
    required this.imageUrl,
    required this.discordChannel,
    required this.foundAt,
    this.isImportant = false,
  });

  double get potentialProfit => estimatedResell - price;
}

// --- MOCK REPOSITORY (Simulated GitHub/Discord Data) ---

class DataProvider {
  static List<ClothingPiece> getItems() {
    return [
      ClothingPiece(
        id: '1',
        brand: 'Gucci',
        name: 'Monogram Canvas Jacket',
        price: 150.00,
        estimatedResell: 450.00,
        imageUrl: 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=500',
        discordChannel: '#designer-steals',
        foundAt: DateTime.now().subtract(const Duration(minutes: 5)),
        isImportant: true,
      ),
      ClothingPiece(
        id: '2',
        brand: 'Nike',
        name: 'Vintage 90s Windbreaker',
        price: 25.00,
        estimatedResell: 85.00,
        imageUrl: 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500',
        discordChannel: '#vintage-general',
        foundAt: DateTime.now().subtract(const Duration(minutes: 12)),
      ),
      ClothingPiece(
        id: '3',
        brand: 'Gucci',
        name: 'Double G Belt - Black',
        price: 80.00,
        estimatedResell: 210.00,
        imageUrl: 'https://images.unsplash.com/photo-1624222247344-550fb8ec973d?w=500',
        discordChannel: '#accessories',
        foundAt: DateTime.now().subtract(const Duration(hours: 1)),
      ),
      ClothingPiece(
        id: '4',
        brand: 'Prada',
        name: 'Nylon Messenger Bag',
        price: 200.00,
        estimatedResell: 550.00,
        imageUrl: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=500',
        discordChannel: '#high-tier',
        foundAt: DateTime.now().subtract(const Duration(hours: 2)),
        isImportant: true,
      ),
      ClothingPiece(
        id: '5',
        brand: 'Nike',
        name: 'Jordan 1 Chicago Low',
        price: 110.00,
        estimatedResell: 240.00,
        imageUrl: 'https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=500',
        discordChannel: '#sneaker-pings',
        foundAt: DateTime.now().subtract(const Duration(hours: 4)),
      ),
    ];
  }
}

// --- MAIN UI SCREEN ---

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final List<ClothingPiece> allItems = DataProvider.getItems();
  
  // Sorting logic for Tabs
  List<String> get brands => ['All', ...allItems.map((e) => e.brand).toSet().toList()];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: brands.length, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('VINTED BOT TRACKER', 
          style: TextStyle(fontWeight: FontWeight.black, letterSpacing: 1.2)),
        actions: [
          IconButton(icon: const Icon(Icons.filter_list), onPressed: () {}),
          IconButton(icon: const Icon(Icons.refresh), onPressed: () => setState(() {})),
        ],
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          indicatorColor: const Color(0xFF00C2C2),
          tabs: brands.map((b) => Tab(text: b.toUpperCase())).toList(),
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: brands.map((brand) {
          final filteredList = brand == 'All' 
              ? allItems 
              : allItems.where((item) => item.brand == brand).toList();
          
          return ListView.builder(
            padding: const EdgeInsets.symmetric(vertical: 10),
            itemCount: filteredList.length,
            itemBuilder: (context, index) => ItemCard(item: filteredList[index]),
          );
        }).toList(),
      ),
      bottomNavigationBar: BottomNavigationBar(
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Feed'),
          BottomNavigationBarItem(icon: Icon(Icons.star), label: 'Important'),
          BottomNavigationBarItem(icon: Icon(Icons.analytics), label: 'Stats'),
        ],
        selectedItemColor: const Color(0xFF00C2C2),
      ),
    );
  }
}

// --- UI COMPONENT: THE ITEM CARD ---

class ItemCard extends StatelessWidget {
  final ClothingPiece item;

  const ItemCard({super.key, required this.item});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: const Color(0xFF1E1E1E),
        borderRadius: BorderRadius.circular(20),
        border: item.isImportant ? Border.all(color: Colors.amber.withOpacity(0.5), width: 1) : null,
      ),
      child: Column(
        children: [
          Stack(
            children: [
              // Product Image
              ClipRRect(
                borderRadius: const BorderRadius.vertical(top: Radius.circular(20)),
                child: Image.network(
                  item.imageUrl,
                  height: 200,
                  width: double.infinity,
                  fit: BoxFit.cover,
                ),
              ),
              // Channel Badge
              Positioned(
                top: 12,
                left: 12,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.black87,
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Text(item.discordChannel, 
                    style: const TextStyle(fontSize: 10, color: Colors.white70)),
                ),
              ),
              // Profit Badge
              Positioned(
                bottom: 12,
                right: 12,
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(
                    color: Colors.greenAccent.shade700,
                    borderRadius: BorderRadius.circular(12),
                    boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.3), blurRadius: 4)],
                  ),
                  child: Text('+ €${item.potentialProfit.toStringAsFixed(0)} Profit', 
                    style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
                ),
              ),
            ],
          ),
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(item.brand.toUpperCase(), 
                      style: const TextStyle(color: Color(0xFF00C2C2), fontWeight: FontWeight.bold)),
                    Text('${DateTime.now().difference(item.foundAt).inMinutes}m ago',
                      style: const TextStyle(color: Colors.grey, fontSize: 12)),
                  ],
                ),
                const SizedBox(height: 5),
                Text(item.name, 
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w600)),
                const Divider(height: 24, color: Colors.white10),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('VINTED PRICE', style: TextStyle(fontSize: 10, color: Colors.grey)),
                        Text('€${item.price.toStringAsFixed(2)}', 
                          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                      ],
                    ),
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.end,
                      children: [
                        const Text('EST. RESELL', style: TextStyle(fontSize: 10, color: Colors.grey)),
                        Text('€${item.estimatedResell.toStringAsFixed(2)}', 
                          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Colors.amber)),
                      ],
                    ),
                  ],
                ),
                const SizedBox(height: 15),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () {}, // Future: Link to Vinted
                    style: ElevatedButton.styleFrom(
                      backgroundColor: const Color(0xFF00C2C2),
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                    child: const Text('OPEN ON VINTED'),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
