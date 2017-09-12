import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.Charset;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.jar.JarEntry;
import java.util.jar.JarFile;

import org.objectweb.asm.ClassReader;
import org.objectweb.asm.Opcodes;

public class Runner {
	public static void main(String[] args) {
		try {			
			ArrayList<String> lines = new ArrayList<String>();
			lines.addAll(Arrays.asList("import org.junit.runner.RunWith;",
										"import org.junit.runners.Suite;",
										"",
										"@RunWith(Suite.class)",
										"@Suite.SuiteClasses({" ));
			
			JarFile jar = new JarFile("../hadoop-common-3.0.0-alpha4-tests.jar");
			ArrayList<String> testClasses = getTestClasses(jar);
			for (String className : testClasses) {
				lines.add("  " + className);
			}
			
			lines.add("})");
			lines.add("public class AllTests { /* empty */}");	
			
			Path file = Paths.get("AllTests.java");
			Files.write(file, lines, Charset.forName("UTF-8"));
		} catch (Exception e) {
			e.printStackTrace();
		}
		
	}
	
	
	public static ArrayList<String> getTestClasses(JarFile jar) throws IOException {
		ArrayList<String> classNames = new ArrayList<String>();

		// Iterate over the entries in the JAR file
		Enumeration<? extends JarEntry> entries = jar.entries();
		while (entries.hasMoreElements()) {
			JarEntry entry = entries.nextElement();
			
			//System.out.println(entry.getName());
			
			// Skip things which don't end with .class
			if (!entry.getName().endsWith(".class")) {
				continue;
			}
			
			// Open an input stream for the JAR file
			InputStream stream = jar.getInputStream(entry);

			// Create our visitor for testing if a class is a test
			TestVisitor visitor = new TestVisitor(Opcodes.ASM4);

			try {
				
				// See if the class is a unit test class, and add it to the list if it is
				ClassReader reader = new ClassReader(stream);
				reader.accept(visitor, ClassReader.SKIP_CODE);
				if (visitor.isTestClass()) {
					String[] parts = entry.getName().split("/");
					classNames.add(parts[parts.length-1]);
				}
				
			} finally {
				stream.close();
			}
		}

		return classNames;
	} 
}
