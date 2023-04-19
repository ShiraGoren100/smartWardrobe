package com.example.smartwardrobe

import android.graphics.Color
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.navigation.ui.AppBarConfiguration
import com.example.smartwardrobe.databinding.ActivityAddItemBinding
import com.google.android.material.snackbar.Snackbar

class AddItemActivity : AppCompatActivity() {
    private lateinit var appBarConfiguration: AppBarConfiguration
    private lateinit var binding: ActivityAddItemBinding
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityAddItemBinding.inflate(layoutInflater)
        setContentView(binding.root)

//        setSupportActionBar(binding.appBar.toolbar)


//        val categories = resources.getStringArray(R.array.categories)
//        val categories_adapter = ArrayAdapter<String>(this, R.layout.list_item,categories)
//        (binding.categoryInput.editText as? AutoCompleteTextView)?.setAdapter(categories_adapter)

        /*val colors = resources.getStringArray(R.array.colors)
        val colors_adapter = ArrayAdapter<String>(this, R.layout.list_item,colors)
        (binding.colorInput.editText as? AutoCompleteTextView)?.setAdapter(colors_adapter)*/

        val categoryInput = findViewById<AutoCompleteTextView>(R.id.tv_category)
        val categories = resources.getStringArray(R.array.categories)
        val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, categories)
        categoryInput.setAdapter(adapter)

        val featureMap = mutableMapOf<String, List<String>>()

        categories.forEach { category ->
            val featuresResId = resources.getIdentifier("features_$category", "array", packageName)
            val features = resources.getStringArray(featuresResId).toList()
            featureMap[category] = features
        }

        binding.tvCategory.setOnItemClickListener { parent, view, position, id ->
            val category = parent.getItemAtPosition(position).toString()
            val arrayName = "features_$category"
            Log.d("DEBUG", "Category: $category, Array name: $arrayName")
            val features = resources.getStringArray(
                resources.getIdentifier(arrayName, "array", packageName)
            )
            updateFeatures(features)
        }


        binding.tvCategory.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                val selectedCategory = parent?.getItemAtPosition(position).toString()
                val features = featureMap[selectedCategory]
                Snackbar.make(view!!, R.string.app_name, Snackbar.LENGTH_SHORT).show()
                binding.featureContainer.removeAllViews()

                features?.forEach { feature ->
                    val checkBox = CheckBox(this@AddItemActivity)
                    checkBox.text = feature
                    checkBox.layoutParams = LinearLayout.LayoutParams(
                        ViewGroup.LayoutParams.WRAP_CONTENT,
                        ViewGroup.LayoutParams.WRAP_CONTENT
                    )
                    binding.featureContainer.addView(checkBox)
                }

            }

            override fun onNothingSelected(parent: AdapterView<*>?) {}
        }
    }

    private fun updateFeatures(features: Array<String>) {
        binding.featureContainer.removeAllViews()
        features.forEach { feature ->
            val checkBox = CheckBox(this@AddItemActivity)
            checkBox.text = feature
            binding.featureContainer.addView(checkBox)
        }
    }

}