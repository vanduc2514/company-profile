// test-non-existent.js
// Automated test suite verifying detection of fictional, placeholder, and non-existent companies

const testCases = [
  { name: 'acme company', description: 'Fictional/placeholder company from pop culture & demos' },
  { name: 'Dunder Mifflin Paper Co', description: 'Fictional paper company from TV show The Office' },
  { name: 'Wayne Enterprises', description: 'Fictional multinational conglomerate from Batman / DC Comics' },
  { name: 'Stark Industries', description: 'Fictional enterprise from Marvel Comics' },
  { name: 'Initech Corporation', description: 'Fictional software company from Office Space' },
  { name: 'Umbrella Corporation', description: 'Fictional pharmaceutical/biotech company from Resident Evil' },
  { name: 'Hooli Inc', description: 'Fictional tech giant from Silicon Valley TV series' },
  { name: 'Vandelay Industries', description: 'Fictional latex export company from Seinfeld' },
  { name: 'Soylent Corporation', description: 'Fictional food manufacturing conglomerate from Soylent Green' },
  { name: 'Cyberdyne Systems', description: 'Fictional defense & cybernetics company from Terminator' },
  { name: 'Los Pollos Hermanos', description: 'Fictional fast food chain from Breaking Bad / Better Call Saul' },
  { name: 'Buy n Large Corp', description: 'Fictional megacorporation from WALL-E / Pixar' },
  { name: 'Demo Test Company ABC 123', description: 'Generic placeholder / dummy company name' },
  { name: 'asdfghjkl zxcvbnm', description: 'Random keyboard mash / meaningless gibberish string' }
];

async function runTests() {
  console.log('===============================================================');
  console.log('🧪 AUTOMATED TEST: NON-EXISTENT & FICTIONAL COMPANY DETECTION');
  console.log('===============================================================\n');

  let passed = 0;
  let failed = 0;

  for (let i = 0; i < testCases.length; i++) {
    const { name, description } = testCases[i];
    try {
      const response = await fetch('http://localhost:3000/api/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ companyName: name })
      });

      const data = await response.json();

      if (data && data.found === false) {
        console.log(`✅ [PASS] #${i + 1}: "${name}"`);
        console.log(`   └─ Type: ${description}`);
        console.log(`   └─ Response status: found=false`);
        console.log(`   └─ Vietnamese Message: "${data.message}"\n`);
        passed++;
      } else {
        console.log(`❌ [FAIL] #${i + 1}: "${name}"`);
        console.log(`   └─ Type: ${description}`);
        console.log(`   └─ Expected found=false, but got found=${data?.found}`);
        console.log(`   └─ Profile Created:`, data?.id, data?.companyName, '\n');
        failed++;
      }
    } catch (err) {
      console.error(`❌ [ERROR] #${i + 1}: "${name}":`, err.message);
      failed++;
    }
  }

  // Also verify a real legitimate company returns found: true
  console.log('---------------------------------------------------------------');
  console.log('🔍 CONTROL TEST: LEGITIMATE OPERATING COMPANY (POSITIVE CONTROL)');
  console.log('---------------------------------------------------------------');
  try {
    const realResponse = await fetch('http://localhost:3000/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ companyName: 'Stripe Inc' })
    });
    const realData = await realResponse.json();
    if (realData && realData.found === true) {
      console.log(`✅ [PASS] Positive Control "Stripe Inc": successfully generated profile (ID: ${realData.id}, Score: ${realData.confidenceScore}%)\n`);
    } else {
      console.log(`❌ [FAIL] Positive Control "Stripe Inc" was unexpectedly rejected.\n`);
    }
  } catch (err) {
    console.error(`❌ [ERROR] Positive Control test failed:`, err.message);
  }

  console.log('===============================================================');
  console.log(`📊 TEST SUMMARY: ${passed}/${testCases.length} NON-REAL COMPANIES REJECTED (${failed === 0 ? '100% SUCCESS' : 'FAILED'})`);
  console.log('===============================================================');

  if (failed > 0) {
    process.exit(1);
  }
}

runTests();
