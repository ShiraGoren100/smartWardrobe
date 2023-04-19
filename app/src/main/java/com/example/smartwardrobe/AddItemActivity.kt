package com.example.smartwardrobe
import com.google.android.material.R.style.Widget_MaterialComponents_TextInputLayout_OutlinedBox_ExposedDropdownMenu

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.widget.*
import androidx.navigation.ui.AppBarConfiguration
import com.example.smartwardrobe.databinding.ActivityAddItemBinding
import com.google.android.material.textfield.TextInputLayout

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
            val categoryResId = resources.getIdentifier("category_$category", "array", packageName)
            val categor = resources.getStringArray(categoryResId).toList()
            featureMap[category] = categor
        }

        binding.tvCategory.setOnItemClickListener { parent, view, position, id ->
            val category = parent.getItemAtPosition(position).toString()
            val arrayName = "category_$category"
            Log.d("DEBUG", "Category: $category, Array name: $arrayName")
            val features = resources.getStringArray(
                resources.getIdentifier(arrayName, "array", packageName)
            )
            updateFeatures(features)
        }

/*
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
*/
    }

    private fun updateFeatures(features: Array<String>) {
        binding.featureContainer.removeAllViews()
        features?.forEach { feature ->
            val featureInputLayout = LayoutInflater.from(this@AddItemActivity)
                .inflate(R.layout.item_spinner, null) as TextInputLayout

            featureInputLayout.hint = feature
            val properties = resources.getStringArray(resources.getIdentifier("feature_$feature", "array", packageName))

            val featureAutoCompleteTextView = featureInputLayout.findViewById<AutoCompleteTextView>(R.id.tv_feature)
            val adapter = ArrayAdapter(
                this@AddItemActivity,
                android.R.layout.simple_spinner_dropdown_item,
                properties
            )
            featureAutoCompleteTextView.setAdapter(adapter)
            featureAutoCompleteTextView.dropDownAnchor = featureInputLayout.id

            binding.featureContainer.addView(featureInputLayout)
        }
    }



}