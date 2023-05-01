package com.example.smartwardrobe.ui.closet

import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ArrayAdapter

import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager

import com.example.smartwardrobe.R
import com.example.smartwardrobe.data.ClothingItem
import com.example.smartwardrobe.data.Property
import com.example.smartwardrobe.databinding.FragmentClosetBinding
import com.google.gson.Gson

class ClosetFragment : Fragment() {

    private var _binding: FragmentClosetBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!
    private lateinit var items: ArrayList<ClothingItem>
    private lateinit var itemsAdapter: ClothingAdapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val closetViewModel =
            ViewModelProvider(this).get(ClosetViewModel::class.java)

        _binding = FragmentClosetBinding.inflate(inflater, container, false)
        val root: View = binding.root

        items = ArrayList<ClothingItem>()
//        binding.clothes.layoutManager = LinearLayoutManager(activity)
        itemsAdapter = ClothingAdapter(items)

        val categoryInput = binding.tvCategory
        val categories = resources.getStringArray(R.array.categories)
        val categoryAdapter = context?.let { ArrayAdapter(it, android.R.layout.simple_list_item_1, categories) }
        categoryInput.setAdapter(categoryAdapter)
//        categories.forEach { category ->
//            val categoryResId = resources.getIdentifier("category_$category", "array", packageName)
//            val categor = resources.getStringArray(categoryResId).toList()
//        }

        binding.tvCategory.setOnItemClickListener { parent, view, position, id ->
            val category = parent.getItemAtPosition(position).toString()
            val arrayName = "category_$category"
            Log.d("DEBUG", "Category: $category, Array name: $arrayName")
            val features = resources.getStringArray(
                resources.getIdentifier(arrayName, "array", requireActivity().packageName)
            )
            items.clear()
            items = getList("$category")


        }

//        val textView: TextView = binding.textGallery
//        closetViewModel.text.observe(viewLifecycleOwner) {
//            textView.text = it
//        }
        return root
    }

    private fun getList(category: String): ArrayList<ClothingItem> {
        val dataStr =
            """[{ "id":"1", "img": "string", "category": "Shirts", "color": "blue", "Sleeves": "Sleeveless", "Weather": "Heat wave", "Thickness": "Light" }, { "id":2, "img": "string", "category": "Shirts", "color": "blue", "Sleeves": "Sleeveless", "Weather": "Heat wave", "Thickness": "Light" }, { "id":3, "img": "string", "category": "Shirts", "color": "blue", "Sleeves": "Sleeveless", "Weather": "Heat wave", "Thickness": "Light" }]"""
        val gson = Gson()
        val data = gson.fromJson(dataStr, Array<Map<String, String>>::class.java).toList()
        return data.map { map ->
            ClothingItem(
                map["id"]!!.toInt(),
                map["img"]!!,
                listOf(
                    Property("category", map["category"]!!),
                    Property("color", map["color"]!!),
                    Property("Sleeves", map["Sleeves"]!!),
                    Property("Weather", map["Weather"]!!),
                    Property("Thickness", map["Thickness"]!!)
                )
            )
        }.toCollection(ArrayList())
    }


    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}