import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';

dotenv.config();

const supabaseUrl = process.env.VITE_SUPABASE_URL;
const supabaseKey = process.env.VITE_SUPABASE_ANON;
console.log(supabaseUrl);
console.log(supabaseKey);
console.log('Testing Supabase connection...');

const supabase = createClient(supabaseUrl, supabaseKey);

async function testTable() {
  try {
    // Test 1: Check if table exists by trying to get schema
    console.log('\n=== Testing Table Existence ===');
    
    const { data, error } = await supabase
      .from('all_reviews')
      .select('*')
      .limit(10);
    
    if (error) {
      console.error('❌ Table error:', error.message);
      console.log('💡 This means the table "all_reviews" does not exist yet.');
      console.log('📋 You need to create the table in your Supabase dashboard.');
      return;
    }
    
    console.log('✅ Table exists! Sample data:', data);
    
    // Test 2: Count total records
    const { count, error: countError } = await supabase
      .from('all_reviews')
      .select('*', { count: 'exact', head: true });
    
    if (countError) {
      console.error('Count error:', countError);
    } else {
      console.log('📊 Total records:', count);
    }
    
  } catch (err) {
    console.error('Unexpected error:', err);
  }
}

testTable(); 