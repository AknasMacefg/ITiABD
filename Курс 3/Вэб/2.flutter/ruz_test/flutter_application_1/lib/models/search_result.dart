class SearchResult {
  final String id;
  final String label;
  final String description;
  final String type;

  SearchResult({
    required this.id,
    required this.label,
    required this.description,
    required this.type,
  });

  factory SearchResult.fromJson(Map<String, dynamic> json) {
    return SearchResult(
      id: (json['id'] ?? '').toString(),
      label: (json['label'] ?? '').toString(),
      description: (json['description'] ?? '').toString(),
      type: (json['type'] ?? '').toString(),
    );
  }

  @override
  String toString() => label;

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is SearchResult && id == other.id && type == other.type;

  @override
  int get hashCode => id.hashCode ^ type.hashCode;
}
