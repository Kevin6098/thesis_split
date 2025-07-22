import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

const supabaseUrl = process.env.VITE_SUPABASE_URL;
const supabaseKey = process.env.VITE_SUPABASE_ANON;

console.log('Supabase URL:', supabaseUrl);
console.log('Supabase Key:', supabaseKey ? 'Present' : 'Missing');

if (!supabaseUrl || !supabaseKey) {
  console.error('Missing Supabase credentials');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

async function testConnection() {
  try {
    console.log('\n=== Testing Supabase Connection ===');
    
    // Test 1: Basic connection - get table info
    const { data: tables, error: tablesError } = await supabase
      .from('all_reviews')
      .select('*')
      .limit(1);
    
    if (tablesError) {
      console.error('Table access error:', tablesError);
      return;
    }
    
    console.log('✅ Connection successful! Sample data:', tables);
    
    // Test 2: Count total records
    const { count, error: countError } = await supabase
      .from('all_reviews')
      .select('*', { count: 'exact', head: true });
    
    if (countError) {
      console.error('Count error:', countError);
    } else {
      console.log('📊 Total records in database:', count);
    }
    
    // Test 3: Search for "並"
    console.log('\n=== Testing search for "並" ===');
    const { data: searchResults, count: searchCount, error: searchError } = await supabase
      .from('all_reviews')
      .select('*', { count: 'exact' })
      .ilike('comment', '%並%');
    
    if (searchError) {
      console.error('Search error:', searchError);
    } else {
      console.log('🔍 Search results for "並":', searchCount, 'matches found');
      if (searchResults && searchResults.length > 0) {
        console.log('Sample results:');
        searchResults.slice(0, 3).forEach((result, index) => {
          console.log(`${index + 1}. Dataset: ${result.dataset}`);
          console.log(`   Comment: ${result.comment.substring(0, 100)}...`);
        });
      }
    }
    
    // Test 4: Check what columns exist
    console.log('\n=== Checking table structure ===');
    const { data: structure, error: structureError } = await supabase
      .from('all_reviews')
      .select('*')
      .limit(1);
      
    if (!structureError && structure && structure.length > 0) {
      console.log('📋 Available columns:', Object.keys(structure[0]));
    }
    
  } catch (err) {
    console.error('Unexpected error:', err);
  }
}

testConnection(); 